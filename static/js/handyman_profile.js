
//const id = document.querySelector(".profile-button").name;
//console.log(id)
document.querySelector(".profile-button").addEventListener('click', goToCompany);

function goToCompany () {
    const id = document.querySelector(".profile-button").name;
    location.replace(`/search_result/${id}`);
}