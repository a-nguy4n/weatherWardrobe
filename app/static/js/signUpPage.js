// document.getElementById('signUpForm').addEventListener('submit', async function(event){

//     event.preventDefault();

//     const firstName = document.getElementById('firstName').value;
//     const lastName = document.getElementById('lastName').value;
//     const email = document.getElementById('email').value;
//     const password = document.getElementById('passwordSignUp').value; 
//     const validatePassword = document.getElementById('passwordVerify').value;

//     // checking for input fields not empty 
//     if(!firstName || !lastName || !email || !password){
//         alert("All fields are required. Please fill in missing fields.");
//         return;
//     }

//     //Password Length Validation 
//     if(password.length < 8){
//         alert("Password must be at least 8 characters long.");
//         return;
//     }

//     // Validate Password to match
//     if(password != validatePassword){
//         alert("Passwords do not match");
//         return;
//     }

//     const formData = new FormData(this);

//     console.log(formData);

//     try {
//         const response = await fetch("/signup", {
//             method: 'POST',
//             body: formData
//         });
//     } 
//     catch (error) {
//         console.error("Error submitting form:", error);
//         alert("Something went wrong. Please try again.");
//     }


// // // // grabbing users from Local Storage
// // // const users = JSON.parse(localStorage.getItem('users')) || [];

// // // // searching user with matching email
// // // const user = users.find(u => u.email === email && u.password === password);

// // // // saving user sign up in & redirect to login page 
// // // if(user){

// // //     localStorage.setItem('loggedInUser', JSON.stringify(user));
// // //     alert("Successful Login!");

// // //     // redirection to page after Sign Up
// // //     setTimeout(() => {
// // //         window.location.href = '/app/templates/loginPage.html'

// // //     }, 1000);
// // // }

// // // else{ 
// // //     alert('Invalid username or password');
// // // }
// });