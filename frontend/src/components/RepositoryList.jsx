function RepositoryList({
  repositories,
}) {
  return (
    <div>
      <h2>
        My Repositories
      </h2>

      {repositories.map(
        (repo) => (
          <div key={repo.id}>
            <p>
              {
                repo.repository_name
              }
            </p>
          </div>
        )
      )}
    </div>
  );
}

export default RepositoryList;