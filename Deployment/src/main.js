// import { Clerk } from '@clerk/clerk-js'

// const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

// const clerk = new Clerk(clerkPubKey)
// await clerk.load()

// if (clerk.user) {
//   document.getElementById('important').innerHTML = `
//     <div id="user-button"></div>
//   `

//   const userButtonDiv = document.getElementById('user-button')

//   clerk.mountUserButton(userButtonDiv)
// } else {
//   document.getElementById('important').innerHTML = `
//     <div id="sign-in"></div>
//   `

//   const signInDiv = document.getElementById('sign-in')

//   clerk.mountSignIn(signInDiv)
// }


import { Clerk } from '@clerk/clerk-js';

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

const clerk = new Clerk(clerkPubKey);

await clerk.load();

if (clerk.user) {
  // If the user is logged in, hide the trigger buttons
  document.getElementById('sign-up-trigger').style.display = 'none';
  document.getElementById('sign-in-trigger').style.display = 'none';
} else {
  // Show the SignUp and SignIn buttons if the user is not logged in
  document.getElementById('sign-up-trigger').style.display = 'block';
  document.getElementById('sign-in-trigger').style.display = 'block';

  // Event listeners for opening the Clerk modals
  document.getElementById('sign-up-trigger').addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default link behavior
    clerk.openSignUp();
  });

  document.getElementById('sign-in-trigger').addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default link behavior
    clerk.openSignIn();
  });
}

