import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Office } from '../services/api';

interface MapViewProps {
  userLocation: { latitude: number; longitude: number } | null;
  offices: Office[];
  selectedOfficeId?: number | null;
  onSelectOffice?: (office: Office) => void;
}

export const WelfareMap: React.FC<MapViewProps> = ({
  userLocation,
  offices,
  selectedOfficeId,
  onSelectOffice
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markersRef = useRef<{ [key: string]: L.Marker }>({});

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      const initialLat = userLocation ? userLocation.latitude : 12.9716;
      const initialLng = userLocation ? userLocation.longitude : 77.5946;

      const map = L.map(mapContainerRef.current, {
        center: [initialLat, initialLng],
        zoom: 11,
        zoomControl: true,
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">OpenStreetMap</a> contributors',
        maxZoom: 18,
      }).addTo(map);

      mapInstanceRef.current = map;
    }

    return () => {
      // Cleanup on unmount
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Update markers and bounds when userLocation or offices change
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    // Remove existing markers
    Object.values(markersRef.current).forEach(marker => marker.remove());
    markersRef.current = {};

    const bounds = L.latLngBounds([]);

    // 1. Citizen marker
    if (userLocation) {
      const userIcon = L.divIcon({
        className: 'user-gps-marker',
        html: `
          <div style="
            background: #2563eb;
            color: #ffffff;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid #ffffff;
            box-shadow: 0 0 10px rgba(37,99,235,0.7);
            font-size: 14px;
          ">
            📍
          </div>
        `,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
        popupAnchor: [0, -14],
      });

      const userMarker = L.marker([userLocation.latitude, userLocation.longitude], {
        icon: userIcon,
        zIndexOffset: 1000,
      }).addTo(map);

      userMarker.bindPopup(`
        <div style="padding: 4px; font-family: inherit;">
          <strong style="color: #1e3a8a; font-size: 13px;">📍 Your Current Location</strong>
          <div style="font-size: 11px; color: #475569; margin-top: 3px;">
            Lat: ${userLocation.latitude.toFixed(4)}, Lon: ${userLocation.longitude.toFixed(4)}
          </div>
          <div style="font-size: 11px; color: #15803d; font-weight: 600; margin-top: 3px;">
            Verified GPS coordinates
          </div>
        </div>
      `);

      markersRef.current['user'] = userMarker;
      bounds.extend([userLocation.latitude, userLocation.longitude]);
    }

    // 2. Office markers
    offices.forEach(office => {
      if (office.latitude && office.longitude) {
        const isSelected = selectedOfficeId === office.id;
        const isDistrict = office.office_type.includes('District');
        const bg = isSelected ? '#ea580c' : isDistrict ? '#1d4ed8' : '#15803d';

        const officeIcon = L.divIcon({
          className: 'swd-office-marker',
          html: `
            <div style="
              background: ${bg};
              color: #ffffff;
              width: 32px;
              height: 32px;
              border-radius: 8px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: 2px solid #ffffff;
              box-shadow: 0 2px 6px rgba(0,0,0,0.3);
              font-size: 14px;
              cursor: pointer;
            ">
              🏛️
            </div>
          `,
          iconSize: [32, 32],
          iconAnchor: [16, 16],
          popupAnchor: [0, -16],
        });

        const marker = L.marker([office.latitude, office.longitude], { icon: officeIcon }).addTo(map);

        marker.bindPopup(`
          <div style="padding: 4px 6px; font-family: inherit; max-width: 260px;">
            <div style="font-size: 10px; font-weight: 700; color: ${isDistrict ? '#1d4ed8' : '#15803d'}; text-transform: uppercase;">
              ${office.office_type} &bull; ${office.verification_status}
            </div>
            <strong style="font-size: 13px; color: #0f172a; display: block; margin: 2px 0 4px;">
              ${office.name}
            </strong>
            ${office.distance_km !== undefined ? `
              <div style="font-size: 12px; font-weight: 700; color: #ea580c; margin-bottom: 4px;">
                ⚡ ${office.distance_km} km away
              </div>
            ` : ''}
            <div style="font-size: 11px; color: #475569; margin-bottom: 4px; line-height: 1.3;">
              ${office.address}
            </div>
            <div style="font-size: 11px; color: #334155; margin-bottom: 2px;">
              <strong>Phone:</strong> ${office.contact_number}
            </div>
            <div style="font-size: 11px; color: #334155; margin-bottom: 2px;">
              <strong>Hours:</strong> ${office.working_hours}
            </div>
            <div style="margin-top: 6px; font-size: 10px; background: #f1f5f9; padding: 4px; border-radius: 4px;">
              <strong>Services:</strong> ${office.services_offered}
            </div>
          </div>
        `);

        marker.on('click', () => {
          if (onSelectOffice) onSelectOffice(office);
        });

        markersRef.current[`office-${office.id}`] = marker;
        bounds.extend([office.latitude, office.longitude]);
      }
    });

    // Fit map bounds if points exist
    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 });
    }
  }, [userLocation, offices, selectedOfficeId, onSelectOffice]);

  // If selectedOfficeId changes, open popup and pan to it
  useEffect(() => {
    if (selectedOfficeId && markersRef.current[`office-${selectedOfficeId}`] && mapInstanceRef.current) {
      const marker = markersRef.current[`office-${selectedOfficeId}`];
      marker.openPopup();
      mapInstanceRef.current.setView(marker.getLatLng(), 14, { animate: true });
    }
  }, [selectedOfficeId]);

  return (
    <div 
      ref={mapContainerRef} 
      style={{
        width: '100%',
        height: '420px',
        borderRadius: '10px',
        border: '1px solid var(--line)',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
        marginBottom: '1.5rem',
        zIndex: 1,
      }}
    />
  );
};
