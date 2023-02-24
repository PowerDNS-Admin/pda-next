import React from "react";

const LoadError = function() {
  return (
    <section className="app-card">
      <h2 className="pg-subtitle">{gettext("Sorry, there was an error loading your data.")}</h2>
      <div className="pg-content">
        <p>
          {gettext("Check your internet connection and try reloading the page.")}
        </p>
        <p>
          {gettext("If you are the site administrator and setting up your site for the first time, see the documentation to resolve this: ")}
          <a href="https://docs.saaspegasus.com/apis.html#api-client-requests-are-failing" target="_blank">
            {gettext("Troubleshooting API errors.")}
          </a>
        </p>
      </div>
    </section>
  );
};

export default LoadError;
