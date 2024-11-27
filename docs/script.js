/**
 * script.js - Main JavaScript file for the LHSCC Discord Bot documentation website
 * 
 * This file handles the interactive features of the documentation website including:
 * - Smooth scrolling navigation
 * - Active navigation link highlighting based on scroll position
 * 
 * @author D4LM
 * @version 1.0.0
 */

/**
 * Implements smooth scrolling behavior for all navigation links
 * that point to page sections (href starting with #)
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

/**
 * Handles the active state of navigation links based on scroll position
 * Adds 'active' class to the navigation link that corresponds to the
 * currently visible section of the page
 */
window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('section');
    
    // Find the current section based on scroll position
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        // Add 60px offset to account for fixed navigation bar
        if (pageYOffset >= sectionTop - 60) {
            current = section.getAttribute('id');
        }
    });

    // Update active state of navigation links
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').substring(1) === current) {
            link.classList.add('active');
        }
    });
});