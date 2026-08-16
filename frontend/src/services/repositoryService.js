import api from "./api";

export async function importRepository(
  githubUrl
) {
  const response =
    await api.post(
      "/repositories/import/",
      {
        github_url: githubUrl,
      }
    );

  return response.data;
}

export async function getRepositories() {
  const response =
    await api.get(
      "/repositories/"
    );

  return response.data;
}