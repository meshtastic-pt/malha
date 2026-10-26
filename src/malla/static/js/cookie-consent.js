/**
 * Consent controller for optional Rybbit analytics.
 * Analytics is disabled by default and loaded only after an explicit opt-in.
 */
(function () {
    'use strict';

    const CONSENT_KEY = 'malla-analytics-consent-v1';
    const RYBBIT_OPTOUT_KEY = 'disable-rybbit';
    const RYBBIT_SCRIPT_ID = 'rybbit-analytics';
    const RYBBIT_SCRIPT_URL = 'https://tracking.tejo.pro/api/script.js?siteId=4fd05c7e8b89';
    const ACCEPTED = 'accepted';
    const REJECTED = 'rejected';

    function readStorage(key) {
        try {
            return window.localStorage.getItem(key);
        } catch (_error) {
            return null;
        }
    }

    function writeStorage(key, value) {
        try {
            window.localStorage.setItem(key, value);
        } catch (_error) {
            // The choice still applies to the current page when storage is unavailable.
        }
    }

    function removeStorage(key) {
        try {
            window.localStorage.removeItem(key);
        } catch (_error) {
            // Ignore browsers where persistent storage is unavailable.
        }
    }

    function loadAnalytics() {
        if (document.getElementById(RYBBIT_SCRIPT_ID)) {
            return;
        }

        window.__RYBBIT_OPTOUT__ = false;
        removeStorage(RYBBIT_OPTOUT_KEY);

        const script = document.createElement('script');
        script.id = RYBBIT_SCRIPT_ID;
        script.src = RYBBIT_SCRIPT_URL;
        script.defer = true;
        document.head.appendChild(script);
    }

    function disableAnalytics() {
        window.__RYBBIT_OPTOUT__ = true;
        writeStorage(RYBBIT_OPTOUT_KEY, 'true');

        if (window.rybbit && typeof window.rybbit.cleanup === 'function') {
            window.rybbit.cleanup();
        }

        const script = document.getElementById(RYBBIT_SCRIPT_ID);
        if (script) {
            script.remove();
        }
    }

    function initializeConsent() {
        const banner = document.getElementById('cookie-consent');
        const acceptButton = document.getElementById('cookie-consent-accept');
        const rejectButton = document.getElementById('cookie-consent-reject');
        const settingsButton = document.getElementById('cookie-settings-button');

        if (!banner || !acceptButton || !rejectButton) {
            disableAnalytics();
            return;
        }

        const hideBanner = () => {
            banner.hidden = true;
        };

        const showBanner = (moveFocus) => {
            banner.hidden = false;
            if (moveFocus) {
                rejectButton.focus();
            }
        };

        const saveChoice = (choice) => {
            writeStorage(CONSENT_KEY, choice);

            if (choice === ACCEPTED) {
                loadAnalytics();
            } else {
                disableAnalytics();
            }

            hideBanner();
        };

        acceptButton.addEventListener('click', () => saveChoice(ACCEPTED));
        rejectButton.addEventListener('click', () => saveChoice(REJECTED));

        if (settingsButton) {
            settingsButton.addEventListener('click', () => showBanner(true));
        }

        const savedChoice = readStorage(CONSENT_KEY);
        if (savedChoice === ACCEPTED) {
            loadAnalytics();
        } else if (savedChoice === REJECTED) {
            disableAnalytics();
        } else {
            disableAnalytics();
            showBanner(false);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeConsent, { once: true });
    } else {
        initializeConsent();
    }
}());
