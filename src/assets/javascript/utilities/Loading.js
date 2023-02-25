import React from "react";

const LoadingScreen = function() {
  return (
    <div className='app-card pg-text-centered'>
      <div className="lds-ripple"><div></div><div></div></div>
      <p className="heading has-text-primary">Loading...</p>
    </div>
  )
};

export default LoadingScreen;
