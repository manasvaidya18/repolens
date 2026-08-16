import { useState } from "react";

function RegisterForm({
  onRegister,
  switchToLogin,
}) {
  const [email, setEmail] =
    useState("");

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  function handleSubmit(event) {
    event.preventDefault();

    onRegister(
      email,
      username,
      password
    );
  }

  return (
    <div className="auth-container">
      <h2>Create Account</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
        setEmail(
        e.target.value.toLowerCase()
         )
            }
        />

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button type="submit">
          Create Account
        </button>
      </form>

      <p>
        Already have an account?{" "}
        <button
          type="button"
          onClick={switchToLogin}
        >
          Login
        </button>
      </p>
    </div>
  );
}

export default RegisterForm;