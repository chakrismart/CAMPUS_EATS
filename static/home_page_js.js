document.addEventListener('DOMContentLoaded', () => {
    const toggleThemeButton = document.getElementById('toggle_theme');
    const themeIcon = document.getElementById('theme_icon');

    if (!toggleThemeButton || !themeIcon) {
        console.error("Theme toggle button or icon not found!");
        return;
    }

    // Get image paths from HTML attributes
    const lightIcon = themeIcon.getAttribute("data-light");
    const darkIcon = themeIcon.getAttribute("data-dark");

    // Get saved theme or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    setTheme(currentTheme);

    toggleThemeButton.addEventListener('click', () => {
        const theme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
        setTheme(theme);
    });

    function setTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            themeIcon.src = darkIcon;
        } else {
            document.body.classList.remove('dark-theme');
            themeIcon.src = lightIcon;
        }
        localStorage.setItem('theme', theme);
    }
});
