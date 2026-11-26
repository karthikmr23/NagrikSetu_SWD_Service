import React from 'react';
import { DynamicFormField } from '../services/api';

interface DynamicFormProps {
  fields: DynamicFormField[];
  formData: Record<string, any>;
  onChange: (fieldName: string, value: any) => void;
}

export const DynamicFormRenderer: React.FC<DynamicFormProps> = ({
  fields,
  formData,
  onChange
}) => {
  if (!fields || fields.length === 0) {
    return (
      <div style={{ padding: '1rem', background: '#f8fafc', borderRadius: '6px', border: '1px solid var(--line)', color: '#64748b', fontSize: '0.85rem' }}>
        No specialized scheme questions required. Standard eligibility verification applies.
      </div>
    );
  }

  // Sort by display_order
  const sortedFields = [...fields].sort((a, b) => (a.display_order || 0) - (b.display_order || 0));

  return (
    <div className="form-grid-2">
      {sortedFields.map(field => {
        const val = formData[field.field_name] !== undefined ? formData[field.field_name] : '';
        const normalizedType = (field.field_type || 'text').toLowerCase();
        const isFullWidth = normalizedType === 'textarea' || normalizedType === 'radio' || normalizedType === 'checkbox';

        // Dropdown Select
        if (normalizedType === 'select') {
          const options: string[] = Array.isArray(field.options_json) ? field.options_json : [];
          return (
            <div key={field.id} className="form-group">
              <label htmlFor={`field-${field.field_name}`} className="form-label">
                <span>{field.field_label}</span>
                {field.is_required ? (
                  <span className="form-label-required" title="Required field">*</span>
                ) : (
                  <span className="form-label-optional">(Optional)</span>
                )}
              </label>
              <select 
                id={`field-${field.field_name}`}
                className="form-input form-select"
                value={val}
                onChange={e => onChange(field.field_name, e.target.value)}
                required={field.is_required}
              >
                <option value="">-- Select {field.field_label} --</option>
                {options.map((opt, idx) => (
                  <option key={idx} value={opt}>{opt}</option>
                ))}
              </select>
              {field.help_text ? (
                <div className="form-help-text">{field.help_text}</div>
              ) : null}
            </div>
          );
        }

        // Radio Group
        if (normalizedType === 'radio') {
          const options: string[] = Array.isArray(field.options_json) ? field.options_json : [];
          return (
            <div key={field.id} className="form-group form-grid-full">
              <label className="form-label">
                <span>{field.field_label}</span>
                {field.is_required ? (
                  <span className="form-label-required" title="Required field">*</span>
                ) : (
                  <span className="form-label-optional">(Optional)</span>
                )}
              </label>
              <div className="form-radio-group" role="radiogroup" aria-label={field.field_label}>
                {options.map((opt, idx) => {
                  const isChecked = val === opt;
                  return (
                    <label 
                      key={idx} 
                      className={`form-radio-pill ${isChecked ? 'selected' : ''}`}
                    >
                      <input 
                        type="radio" 
                        name={field.field_name} 
                        value={opt} 
                        checked={isChecked} 
                        onChange={() => onChange(field.field_name, opt)}
                        required={field.is_required && !val}
                      />
                      <span>{opt}</span>
                    </label>
                  );
                })}
              </div>
              {field.help_text ? (
                <div className="form-help-text">{field.help_text}</div>
              ) : null}
            </div>
          );
        }

        // Checkbox
        if (normalizedType === 'checkbox') {
          const options: string[] = Array.isArray(field.options_json) ? field.options_json : [];
          const optLabel = options.length > 0 ? options[0] : field.field_label;
          const isChecked = val === true || val === 'true';
          return (
            <div key={field.id} className="form-group form-grid-full">
              <label 
                htmlFor={`chk-${field.id}`}
                className={`form-checkbox-container ${isChecked ? 'checked' : ''}`}
              >
                <input 
                  type="checkbox" 
                  id={`chk-${field.id}`}
                  checked={isChecked}
                  onChange={e => onChange(field.field_name, e.target.checked)}
                  required={field.is_required}
                />
                <span className="form-checkbox-label">
                  <strong>{optLabel}</strong>
                  {field.is_required && <span className="form-label-required"> *</span>}
                  {field.help_text && (
                    <span style={{ display: 'block', fontSize: '0.76rem', color: '#64748b', marginTop: '0.2rem' }}>
                      {field.help_text}
                    </span>
                  )}
                </span>
              </label>
            </div>
          );
        }

        // Textarea
        if (normalizedType === 'textarea') {
          return (
            <div key={field.id} className="form-group form-grid-full">
              <label htmlFor={`field-${field.field_name}`} className="form-label">
                <span>{field.field_label}</span>
                {field.is_required ? (
                  <span className="form-label-required" title="Required field">*</span>
                ) : (
                  <span className="form-label-optional">(Optional)</span>
                )}
              </label>
              <textarea 
                id={`field-${field.field_name}`}
                className="form-input"
                rows={3}
                placeholder={field.placeholder || `Enter ${field.field_label.toLowerCase()}`}
                value={val}
                onChange={e => onChange(field.field_name, e.target.value)}
                required={field.is_required}
              />
              {field.help_text ? (
                <div className="form-help-text">{field.help_text}</div>
              ) : null}
            </div>
          );
        }

        // Date input
        if (normalizedType === 'date') {
          return (
            <div key={field.id} className="form-group">
              <label htmlFor={`field-${field.field_name}`} className="form-label">
                <span>{field.field_label}</span>
                {field.is_required ? (
                  <span className="form-label-required" title="Required field">*</span>
                ) : (
                  <span className="form-label-optional">(Optional)</span>
                )}
              </label>
              <input 
                id={`field-${field.field_name}`}
                type="date"
                className="form-input"
                value={val}
                onChange={e => onChange(field.field_name, e.target.value)}
                required={field.is_required}
              />
              {field.help_text ? (
                <div className="form-help-text">{field.help_text}</div>
              ) : null}
            </div>
          );
        }

        // Number input
        if (normalizedType === 'number') {
          return (
            <div key={field.id} className="form-group">
              <label htmlFor={`field-${field.field_name}`} className="form-label">
                <span>{field.field_label}</span>
                {field.is_required ? (
                  <span className="form-label-required" title="Required field">*</span>
                ) : (
                  <span className="form-label-optional">(Optional)</span>
                )}
              </label>
              <input 
                id={`field-${field.field_name}`}
                type="number"
                step="any"
                className="form-input"
                placeholder={field.placeholder || `Enter numeric ${field.field_label.toLowerCase()}`}
                value={val}
                onChange={e => onChange(field.field_name, e.target.value === '' ? '' : Number(e.target.value))}
                required={field.is_required}
              />
              {field.help_text ? (
                <div className="form-help-text">{field.help_text}</div>
              ) : null}
            </div>
          );
        }

        // Default Text / Mobile / Email input
        return (
          <div key={field.id} className={`form-group ${isFullWidth ? 'form-grid-full' : ''}`}>
            <label htmlFor={`field-${field.field_name}`} className="form-label">
              <span>{field.field_label}</span>
              {field.is_required ? (
                <span className="form-label-required" title="Required field">*</span>
              ) : (
                <span className="form-label-optional">(Optional)</span>
              )}
            </label>
            <input 
              id={`field-${field.field_name}`}
              type={normalizedType === 'email' ? 'email' : (normalizedType === 'mobile' ? 'tel' : 'text')}
              className="form-input"
              placeholder={field.placeholder || `Enter ${field.field_label.toLowerCase()}`}
              value={val}
              onChange={e => onChange(field.field_name, e.target.value)}
              required={field.is_required}
            />
            {field.help_text ? (
              <div className="form-help-text">{field.help_text}</div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};
