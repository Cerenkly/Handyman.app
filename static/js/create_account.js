const switchers = [...document.querySelectorAll('.switcher')];

switchers.forEach(item => {
	item.addEventListener('click', function() {
		switchers.forEach(item => item.parentElement.classList.remove('is-active'))
		this.parentElement.classList.add('is-active')
	})
});


document.querySelector('#continue').addEventListener('click', function() {
	const handymanForm = document.querySelector('#create-handyman-form');
	handymanForm.classList.add("is-active");
	const buttonHandymanForm = document.querySelector('#create-handyman');
	buttonHandymanForm.classList.remove("hide");
	const userForm = document.querySelector('#user-form');
	userForm.classList.remove("is-active");
	const buttonUserForm = document.querySelector('#create-user');
	buttonUserForm.classList.add("hide");

	const email = document.querySelector('#login-email').value;
	const firstName = document.querySelector('#login-first-name').value;
	const lastName = document.querySelector('#login-last-name').value;
	const address = document.querySelector('#login-address').value;
	const password = document.querySelector('#password').value;
	fetch("/users", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ "email": email , "first_name": firstName, "last_name": lastName, "address": address, "password": password}),
	})
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
		});

});

function goHome() {
	location.replace("/");
}