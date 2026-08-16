import { useState, useEffect } from "react";

import api from "./services/api";

import RepoInput from "./components/RepoInput";
import ImportRepositoryButton from "./components/ImportRepositoryButton";
import StatusCard from "./components/StatusCard";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";

import { STATUS } from "./constants/status";

function App() {
  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const [isLoginMode, setIsLoginMode] =
    useState(true);

  const [url, setUrl] = useState("");

  const [repositoryId, setRepositoryId] =
    useState(null);

  const [jobId, setJobId] =
    useState(null);

  const [repositories, setRepositories] =
    useState([]);

  const [status, setStatus] = useState(
    STATUS.NOT_STARTED
  );

  const isUrlValid =
    url.startsWith("https://github.com/");

  function handleLogout() {
    localStorage.removeItem(
      "access_token"
    );

    setToken(null);
    setRepositoryId(null);
    setJobId(null);
    setRepositories([]);
    setStatus(STATUS.NOT_STARTED);
    setUrl("");
  }

  async function loadRepositories() {
    try {
      const response =
        await api.get(
          "/repositories/"
        );

      setRepositories(
        response.data
      );

    } catch (error) {
      console.log(error);
    }
  }

 async function handleLogin(
  email,
  password
) {
  try {
    const response =
      await api.post(
        "/token/",
        {
          email,
          password,
        }
      );

    const data =
      response.data;

    localStorage.setItem(
      "access_token",
      data.access
    );

    setToken(data.access);

  } catch (error) {

  console.log(
    error.response?.data
  );

  const message =
    error.response?.data?.detail ||
    "Login failed";

  alert(message);
}
}

  async function handleRegister(
    email,
    username,
    password
  ) {
    try {
      const response =
        await api.post(
          "/auth/register/",
          {
            email,
            username,
            password,
          }
        );

      console.log(
        response.data
      );

      alert(
  "Account created successfully! Please check your email to verify your account."
);

      setIsLoginMode(true);

    } catch (error) {
      console.log(error);
    }
  }

  async function handleImportRepository() {
    try {
      const response =
        await api.post(
          "/repositories/import/",
          {
            github_url: url,
          }
        );

      const data =
        response.data;

      console.log(data);

      setRepositoryId(
        data.repository.id
      );

      await loadRepositories();

    } catch (error) {
      console.log(error);
    }
  }

  async function handleStartAnalysis() {
    try {
      const response =
        await api.post(
          "/analysis/start/",
          {
            repository_id:
              repositoryId,
          }
        );

      const data =
        response.data;

      console.log(data);

      setJobId(
        data.analysis_job.id
      );

      setStatus(
        data.analysis_job.status
      );

    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    if (token) {
      loadRepositories();
    }
  }, [token]);

  useEffect(() => {
    if (!jobId) {
      return;
    }

    const intervalId =
      setInterval(
        async () => {
          try {
            const response =
              await api.get(
                `/analysis/${jobId}/`
              );

            const data =
              response.data;

            console.log(
              "Status:",
              data.status
            );

            setStatus(
              data.status
            );

            const terminalStates = [
              STATUS.COMPLETED,
              STATUS.FAILED,
              STATUS.ANALYZING,
            ];

            if (
              terminalStates.includes(
                data.status
              )
            ) {
              clearInterval(
                intervalId
              );
            }

          } catch (error) {
            console.log(error);
          }
        },
        3000
      );

    return () => {
      clearInterval(
        intervalId
      );
    };

  }, [jobId]);

  if (!token) {
    return isLoginMode ? (
      <LoginForm
        onLogin={handleLogin}
        switchToRegister={() =>
          setIsLoginMode(false)
        }
      />
    ) : (
      <RegisterForm
        onRegister={
          handleRegister
        }
        switchToLogin={() =>
          setIsLoginMode(true)
        }
      />
    );
  }

  return (
    <div className="app">
      <h1 className="title">
        RepoLens
      </h1>

      <button
        onClick={handleLogout}
      >
        Logout
      </button>

      <RepoInput
        url={url}
        setUrl={setUrl}
      />

      {url && !isUrlValid && (
        <p className="error-message">
          Please enter a valid
          GitHub repository URL.
        </p>
      )}

      <ImportRepositoryButton
        onImport={
          handleImportRepository
        }
        disabled={!isUrlValid}
      />

      {repositoryId && (
        <>
          <p>
            Repository Imported ✓
          </p>

          <p>
            Repository ID:{" "}
            {repositoryId}
          </p>

          <button
            onClick={
              handleStartAnalysis
            }
          >
            Start Analysis
          </button>
        </>
      )}

      {jobId && (
        <p>
          Analysis Job ID:{" "}
          {jobId}
        </p>
      )}

      <h2>
        My Repositories
      </h2>

      {repositories.map(
        (repo) => (
          <div key={repo.id}>
            <p>
              {repo.github_owner}/
              {
                repo.repository_name
              }
            </p>
          </div>
        )
      )}

      <StatusCard
        status={status}
      />
    </div>
  );
}

export default App;