import React from 'react';
import './Homepage.css'; // Separate CSS file for homepage styles

function Homepage() {
  return (
    <div className="home">
      <section className="intro">
        <p>Erleben Sie den Handel auf einer neuen Ebene mit unseren einzigartigen Funktionen.</p>
      </section>
      <section className="features">
        <h2>Warum unsere App einzigartig ist</h2>
        <ul>
          <li><strong>Sicherheit:</strong> Ihre Daten und Transaktionen sind bei uns sicher.</li>
          <li><strong>Analytik:</strong> Erhalten Sie detaillierte Analysen und Berichte.</li>
          <li><strong>Automatisierung:</strong> Nutzen Sie unsere Bots für automatisierten Handel.</li>
        </ul>
      </section>
      <section className="reviews">
        <h2>Bewertungen</h2>
        <h4>Lesen Sie, was unsere zufriedenen Kunden sagen.</h4>
        <p>"Diese App hat meine Trading-Erfahrung revolutioniert!" - Max M.</p>
        <p>"Sicher, schnell und zuverlässig. Absolut empfehlenswert." - Anna K.</p>
      </section>
      <section className="faq">
        <h2>FAQ der wichtigsten fragen</h2>
        <div className="faq-item">
          <h3>Wie sicher ist die App?</h3>
          <p>Unsere App verwendet die neuesten Sicherheitsstandards, um Ihre Daten zu schützen.</p>
        </div>
        <div className="faq-item">
          <h3>Wie funktionieren die Trading-Bots?</h3>
          <p>Unsere Bots analysieren den Markt in Echtzeit und führen Trades automatisch für Sie durch.</p>
        </div>
      </section>
    </div>
  );
}

export default Homepage;
