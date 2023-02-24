import React from 'react';

export default function(props) {
  if (props.errors) {
    return (
      <p className="pg-help pg-text-danger">
        { props.errors.map((error, i) => {
          return <span key={i}>{error}</span>
        })}
      </p>
    );
  }
  return '';
};
