document.addEventListener('DOMContentLoaded', () => {
    if (!!window.performance && window.performance.navigation.type == 2) {
        window.location.reload(true);
    }
});