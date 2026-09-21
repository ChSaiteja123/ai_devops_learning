const services = [
  { name: "checkout-api", status: "healthy", region: "us-east-1", latency: "142 ms", errors: "0.04%" },
  { name: "catalog-api", status: "healthy", region: "us-east-1", latency: "118 ms", errors: "0.02%" },
  { name: "worker", status: "degraded", region: "us-west-2", latency: "386 ms", errors: "1.80%" },
  { name: "payments-db", status: "healthy", region: "us-east-1", latency: "9 ms", errors: "0.00%" },
];

const deployments = [
  ["checkout-api", "v2.8.1", "12 minutes ago"],
  ["catalog-api", "v4.1.0", "38 minutes ago"],
  ["worker", "v1.9.4", "1 hour ago"],
];

const incidents = [
  { severity: "critical", title: "Checkout error rate elevated", service: "checkout-api", age: "8 min ago" },
  { severity: "warning", title: "Worker queue age above target", service: "worker", age: "22 min ago" },
  { severity: "info", title: "Certificate renewal scheduled", service: "edge-gateway", age: "1 hour ago" },
];

const serviceRows = document.querySelector("#service-rows");
const incidentList = document.querySelector("#incident-list");
const deploymentList = document.querySelector("#deployment-list");
const incidentCount = document.querySelector("#incident-count");
const updatedAt = document.querySelector("#updated-at");

function renderServices(filter = "all") {
  const visibleServices = filter === "all" ? services : services.filter((service) => service.status === filter);
  serviceRows.innerHTML = visibleServices.map((service) => `
    <tr>
      <td class="service-name">${service.name}</td>
      <td><span class="status ${service.status}">${service.status}</span></td>
      <td>${service.region}</td>
      <td>${service.latency}</td>
      <td>${service.errors}</td>
    </tr>
  `).join("");
}

function renderIncidents() {
  incidentList.innerHTML = incidents.map((incident) => `
    <article class="incident ${incident.severity}">
      <h3>${incident.title}</h3>
      <p>${incident.service}</p>
      <p>${incident.age} · ${incident.severity}</p>
    </article>
  `).join("");
  incidentCount.textContent = incidents.length;
}

function renderDeployments() {
  deploymentList.innerHTML = deployments.map(([service, version, time]) => `
    <li><strong>${service} <span class="badge success">passed</span></strong><small>${version} · ${time}</small></li>
  `).join("");
}

document.querySelectorAll("[data-service-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-service-filter]").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    renderServices(button.dataset.serviceFilter);
  });
});

document.querySelector("[data-action='clear-filters']").addEventListener("click", () => {
  document.querySelectorAll("[data-service-filter]").forEach((item) => item.classList.remove("active"));
  document.querySelector("[data-service-filter='all']").classList.add("active");
  renderServices();
});

document.querySelector("[data-action='refresh']").addEventListener("click", (event) => {
  updatedAt.textContent = "Updated just now";
  event.currentTarget.textContent = "Refreshed";
  window.setTimeout(() => { event.currentTarget.textContent = "Refresh data"; }, 1200);
});

document.querySelector("[data-action='theme']").addEventListener("click", (event) => {
  const highContrast = document.documentElement.toggleAttribute("data-theme");
  document.documentElement.setAttribute("data-theme", highContrast ? "contrast" : "standard");
  event.currentTarget.setAttribute("aria-pressed", String(highContrast));
});

renderServices();
renderIncidents();
renderDeployments();
