import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Homepage from '../Components/Homepage';

describe('Homepage Component', () => {
  test('renders homepage with all sections', () => {
    render(<Homepage />);
    
    // Check for intro section
    expect(screen.getByText(/Erleben Sie den Handel auf einer neuen Ebene/i)).toBeInTheDocument();

    // Check for features section
    expect(screen.getByText(/Warum unsere App einzigartig ist/i)).toBeInTheDocument();
    expect(screen.getByText(/Sicherheit:/i)).toBeInTheDocument();
    expect(screen.getByText(/Analytik:/i)).toBeInTheDocument();
    expect(screen.getByText(/Automatisierung:/i)).toBeInTheDocument();

    // Check for reviews section
    expect(screen.getByText(/Bewertungen/i)).toBeInTheDocument();
    expect(screen.getByText(/Lesen Sie, was unsere zufriedenen Kunden sagen/i)).toBeInTheDocument();
    expect(screen.getByText(/Diese App hat meine Trading-Erfahrung revolutioniert!/i)).toBeInTheDocument();
    expect(screen.getByText(/Sicher, schnell und zuverlässig. Absolut empfehlenswert./i)).toBeInTheDocument();

    // Check for FAQ section
    expect(screen.getByText(/FAQ der wichtigsten fragen/i)).toBeInTheDocument();
    expect(screen.getByText(/Wie sicher ist die App?/i)).toBeInTheDocument();
    expect(screen.getByText(/Wie funktionieren die Trading-Bots?/i)).toBeInTheDocument();
  });
});
