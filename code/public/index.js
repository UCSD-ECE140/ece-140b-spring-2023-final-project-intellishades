// document.addEventListener("DOMContentLoaded", init);

// async function init() {
//     await fetch("/protected").then(response => {
//         return response.json();
//     }).then(json => {
//         // Only get section information if the data is not null
//         if(json["message"] == 'Access granted') {
//             let navBar = document.querySelector("nav");
//             navBar.innerHTML = `
//                 <a href="/">Main Page</a> | <a href="/logout">Log Out</a> | 
//                 <a href="/devices">Manage Device</a> | <a href="/dashboard">Profile</a>`;
//         }
//     });
// }