function StatusCard({ status }) {
  const statusMessages = {
    NOT_STARTED: "Waiting for repository...",
    PENDING: "Job queued...",
    CLONING: "Cloning repository...",
    INDEXING: "Indexing files...",
    ANALYZING: "Running analyzers...",
    COMPLETED: "Analysis complete!",
  };

  const statusClass = {
    NOT_STARTED: "status-gray",
    PENDING: "status-yellow",
    CLONING: "status-blue",
    INDEXING: "status-purple",
    ANALYZING: "status-orange",
    COMPLETED: "status-green",
  };

  return (
    <div className="status-card">
      <h3>Analysis Status</h3>

      <h4 className={statusClass[status]}>
        {status}
      </h4>

      <p>{statusMessages[status]}</p>
    </div>
  );
}

export default StatusCard;