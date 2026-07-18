(function () {
  "use strict";

  var agenciesGrid = document.getElementById("agencies-grid");
  var agenciesEmpty = document.getElementById("agencies-empty");
  var filtersEl = document.getElementById("filters");
  var companiesSection = document.getElementById("companies-section");
  var companiesGrid = document.getElementById("companies-grid");

  var state = {
    agencies: [],
    activeCategory: "All",
  };

  function el(tag, opts) {
    var node = document.createElement(tag);
    opts = opts || {};
    if (opts.className) node.className = opts.className;
    if (opts.text != null) node.textContent = opts.text;
    if (opts.attrs) {
      for (var k in opts.attrs) {
        if (Object.prototype.hasOwnProperty.call(opts.attrs, k)) {
          node.setAttribute(k, opts.attrs[k]);
        }
      }
    }
    return node;
  }

  function installCommand(agency) {
    return "fabri new agency --from gh:Rushour0/fabri-rosters/" + agency.path + " " + agency.name;
  }

  function renderAgencyCard(agency) {
    var card = el("article", { className: "card agency-card" });

    var top = el("div", { className: "card-top" });
    top.appendChild(el("span", { className: "tag", text: agency.category || "Uncategorized" }));
    if (agency.self_improving) {
      top.appendChild(el("span", { className: "self-improving", text: "Self-improving" }));
    }
    card.appendChild(top);

    card.appendChild(el("h3", { text: agency.title || agency.name }));
    card.appendChild(el("p", { className: "tagline", text: agency.tagline || "" }));

    var agentsCount = agency.agents != null ? agency.agents : "?";
    var toolsCount = agency.tools != null ? agency.tools : "?";
    var cost = agency.max_cost_usd != null ? "$" + agency.max_cost_usd + "/run" : "no cap set";
    card.appendChild(
      el("p", {
        className: "meta",
        text: agentsCount + " agents · " + toolsCount + " tools · " + cost,
      })
    );

    var install = el("div", { className: "install" });
    install.appendChild(el("p", { className: "install-label", text: "Install" }));
    var cmd = installCommand(agency);
    var cmdBtn = el("button", {
      className: "install-cmd",
      text: cmd,
      attrs: { type: "button", "aria-label": "Copy install command for " + (agency.title || agency.name) },
    });
    cmdBtn.addEventListener("click", function () {
      var reset = function () {
        cmdBtn.textContent = cmd;
        cmdBtn.classList.remove("copied");
      };
      var markCopied = function () {
        cmdBtn.textContent = "Copied";
        cmdBtn.classList.add("copied");
        setTimeout(reset, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(cmd).then(markCopied, markCopied);
      } else {
        markCopied();
      }
    });
    install.appendChild(cmdBtn);
    card.appendChild(install);

    return card;
  }

  function distinctCategories(agencies) {
    var seen = {};
    var out = [];
    agencies.forEach(function (a) {
      var c = a.category || "Uncategorized";
      if (!seen[c]) {
        seen[c] = true;
        out.push(c);
      }
    });
    out.sort();
    return out;
  }

  function renderFilters() {
    filtersEl.innerHTML = "";
    var categories = ["All"].concat(distinctCategories(state.agencies));
    categories.forEach(function (cat) {
      var btn = el("button", {
        className: "chip",
        text: cat,
        attrs: {
          type: "button",
          "aria-pressed": String(cat === state.activeCategory),
        },
      });
      btn.addEventListener("click", function () {
        state.activeCategory = cat;
        renderFilters();
        renderAgencies();
      });
      filtersEl.appendChild(btn);
    });
  }

  function renderAgencies() {
    agenciesGrid.innerHTML = "";
    var list =
      state.activeCategory === "All"
        ? state.agencies
        : state.agencies.filter(function (a) {
            return (a.category || "Uncategorized") === state.activeCategory;
          });

    if (list.length === 0) {
      agenciesEmpty.hidden = false;
      return;
    }
    agenciesEmpty.hidden = true;

    list.forEach(function (agency) {
      agenciesGrid.appendChild(renderAgencyCard(agency));
    });
  }

  function renderCompanyCard(company) {
    var card = el("article", { className: "card company-card" });
    card.appendChild(el("h3", { text: company.title || company.name || "Untitled company" }));
    if (company.positioning) {
      card.appendChild(el("p", { className: "positioning", text: company.positioning }));
    }

    var members = company.member_agencies || company.members || [];
    var nodeCount = company.node_count != null ? company.node_count : members.length;
    var crewLabel =
      nodeCount + " agents across " + (members.length || 0) + (members.length === 1 ? " crew" : " crews");
    card.appendChild(el("p", { className: "meta", text: crewLabel }));

    if (members.length) {
      var list = el("ul", { className: "member-chips" });
      members.forEach(function (m) {
        var name = typeof m === "string" ? m : m.name || m.title || "agency";
        list.appendChild(el("li", { text: name }));
      });
      card.appendChild(list);
    }

    return card;
  }

  function renderCompanies(companies) {
    if (!companies || !companies.length) {
      companiesSection.hidden = true;
      return;
    }
    companiesSection.hidden = false;
    companiesGrid.innerHTML = "";
    companies.forEach(function (company) {
      companiesGrid.appendChild(renderCompanyCard(company));
    });
  }

  function renderError(message) {
    agenciesGrid.innerHTML = "";
    agenciesEmpty.hidden = false;
    agenciesEmpty.textContent = message;
  }

  fetch("../index.json")
    .then(function (res) {
      if (!res.ok) {
        throw new Error("Failed to load index.json (" + res.status + ")");
      }
      return res.json();
    })
    .then(function (data) {
      state.agencies = Array.isArray(data.agencies) ? data.agencies : [];
      renderFilters();
      renderAgencies();
      renderCompanies(data.companies);
    })
    .catch(function (err) {
      renderError("Could not load the roster: " + err.message);
    });
})();
