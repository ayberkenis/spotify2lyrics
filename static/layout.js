const darkBtn = document.querySelector('#theme-btn');
const bodyEl = document.querySelector('body');
const icon = document.getElementById("icon")
const text = document.getElementsByClassName("theme-switcher")
const textNode = document.querySelector("#theme-btn").childNodes[1];
const bgArray = document.getElementsByClassName('bg-light')
const textArray = document.getElementsByClassName('text-dark')



const darkMode = () => {
    bodyEl.classList.toggle('dark-mode')

    if (icon.classList.contains('fa-moon')){
        icon.classList.remove('fa-moon');
        icon.classList.toggle('fa-sun');
        textNode.textContent = "Light Mode"

        } else {
            icon.classList.remove('fa-sun');
            icon.classList.toggle('fa-moon');
            textNode.textContent = "Dark Mode"
        }
    }


darkBtn.addEventListener('click', () => {
    // Get the value of the "dark" item from the local storage on every click
    setDarkMode = localStorage.getItem('dark');

    if(setDarkMode === null) {
        darkMode();
        // Set the value of the itwm to "on" when dark mode is on

    } else {
        darkMode();

        // Set the value of the item to  "null" when dark mode if off
        setDarkMode = localStorage.setItem('dark', null);

    }
});

// Get the value of the "dark" item from the local storage
let setDarkMode = localStorage.getItem('dark');

// Check dark mode is on or off on page reload
if(setDarkMode === 'on') {
    darkMode();
}