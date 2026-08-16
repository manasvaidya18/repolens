import api from "./api";

export async function startAnalysis(
  repositoryId
) {
  const response =
    await api.post(
      "/analysis/start/",
      {
        repository_id:
          repositoryId,
      }
    );

  return response.data;
}

export async function getAnalysis(
  jobId
) {
  const response =
    await api.get(
      `/analysis/${jobId}/`
    );

  return response.data;
}