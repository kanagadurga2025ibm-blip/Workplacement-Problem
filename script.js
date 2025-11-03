// Sample job data
let jobs = [
    {
        title: "Web Developer",
        company: "Tech Solutions",
        location: "New York, USA",
        description: "Build and maintain modern web applications."
    },
    {
        title: "UI/UX Designer",
        company: "Creative Studio",
        location: "London, UK",
        description: "Design user-friendly and visually appealing interfaces."
    },
    {
        title: "Data Analyst",
        company: "FinTech Co.",
        location: "Toronto, Canada",
        description: "Analyze datasets to extract meaningful insights."
    }
];

const jobList = document.getElementById("jobList");
const jobForm = document.getElementById("jobForm");
const searchInput = document.getElementById("searchInput");

// Display jobs
function displayJobs(filteredJobs = jobs) {
    jobList.innerHTML = "";

    if (filteredJobs.length === 0) {
        jobList.innerHTML = "<p>No jobs found.</p>";
        return;
    }

    filteredJobs.forEach((job) => {
        const jobCard = document.createElement("div");
        jobCard.classList.add("job-card");
        jobCard.innerHTML = `
      <h3>${job.title}</h3>
      <p><strong>Company:</strong> ${job.company}</p>
      <p><strong>Location:</strong> ${job.location}</p>
      <p>${job.description}</p>
    `;
        jobList.appendChild(jobCard);
    });
}

// Add a new job
jobForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const newJob = {
        title: document.getElementById("jobTitle").value,
        company: document.getElementById("companyName").value,
        location: document.getElementById("location").value,
        description: document.getElementById("description").value,
    };

    jobs.push(newJob);
    displayJobs();

    jobForm.reset();
    alert("Job added successfully!");
});

// Search filter
searchInput.addEventListener("input", (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filteredJobs = jobs.filter(
        (job) =>
            job.title.toLowerCase().includes(searchTerm) ||
            job.location.toLowerCase().includes(searchTerm)
    );
    displayJobs(filteredJobs);
});

// Initialize page
displayJobs();
