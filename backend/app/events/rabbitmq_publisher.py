import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from app.models import OutboxEvent
from app.core.config import settings

logger = logging.getLogger("swd.rabbitmq")

def create_outbox_event(
    db,
    event_type: str,
    correlation_id: str,
    payload: Dict[str, Any]
) -> OutboxEvent:
    event_id = f"evt_swd_{int(datetime.utcnow().timestamp()*1000)}_{os.urandom(4).hex()}"
    outbox = OutboxEvent(
        event_id=event_id,
        event_type=event_type,
        schema_version="1.0",
        correlation_id=correlation_id,
        payload=payload,
        status="PENDING",
        retry_count=0
    )
    db.add(outbox)
    return outbox

def publish_event_to_broker(
    event_type: str, 
    correlation_id: str, 
    payload: Dict[str, Any],
    event_id: Optional[str] = None
) -> bool:
    if not event_id:
        event_id = f"evt_swd_{int(datetime.utcnow().timestamp()*1000)}_{os.urandom(4).hex()}"

    if not settings.RABBITMQ_ENABLED:
        logger.info(f"[RABBITMQ STANDALONE LOG] Event {event_type} (ID: {event_id}, Correlation: {correlation_id}): {payload}")
        return True

    try:
        import pika
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials,
            connection_attempts=3,
            retry_delay=2
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange=settings.RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)

        message_envelope = {
            "event_id": event_id,
            "event_type": event_type,
            "schema_version": "1.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "correlation_id": correlation_id,
            "publisher": "swd-service",
            "payload": payload
        }

        routing_key = f"swd.{event_type.lower()}"
        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(message_envelope),
            properties=pika.BasicProperties(
                delivery_mode=2, # make message persistent
                content_type='application/json',
                correlation_id=correlation_id,
                message_id=event_id
            )
        )
        connection.close()
        logger.info(f"Published {event_type} (ID: {event_id}) to RabbitMQ exchange '{settings.RABBITMQ_EXCHANGE}' with key '{routing_key}'")
        return True
    except Exception as e:
        logger.error(f"Failed to publish event {event_type} to RabbitMQ: {e}")
        return False

def process_pending_outbox_events(db, max_batch: int = 20) -> int:
    """
    Processes pending outbox events, publishes them to RabbitMQ,
    and updates their status/retry count (FR-MQ-012 Outbox Processing).
    """
    pending = db.query(OutboxEvent).filter(
        OutboxEvent.status.in_(["PENDING", "RETRY"])
    ).order_by(OutboxEvent.id.asc()).limit(max_batch).all()

    processed_count = 0
    for evt in pending:
        success = publish_event_to_broker(
            event_type=evt.event_type,
            correlation_id=evt.correlation_id,
            payload=evt.payload,
            event_id=evt.event_id
        )
        if success:
            evt.status = "PUBLISHED"
            evt.published_at = datetime.utcnow()
            evt.error_message = None
            processed_count += 1
        else:
            evt.retry_count = (evt.retry_count or 0) + 1
            if evt.retry_count >= 5:
                evt.status = "FAILED"
                evt.error_message = "Max retry attempts (5) exceeded while publishing to RabbitMQ."
            else:
                evt.status = "RETRY"
                evt.error_message = "Transient failure publishing to RabbitMQ. Queued for retry."

    db.commit()
    return processed_count
