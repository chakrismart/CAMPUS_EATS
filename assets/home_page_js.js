document.addEventListener('DOMContentLoaded', (event) => {
    const toggleThemeButton = document.getElementById('toggle_theme');
    const themeIcon = document.getElementById('theme_icon');

    const initialTheme = localStorage.getItem('theme') || 'light';
    setTheme(initialTheme);

    toggleThemeButton.addEventListener('click', () => {
        const newTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
        setTheme(newTheme);
    });

    function setTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
            themeIcon.src = themeIcon.dataset.dark;
        } else {
            document.body.classList.remove('dark-theme');
            themeIcon.src = themeIcon.dataset.light;
        }
        localStorage.setItem('theme', theme);
    }
});