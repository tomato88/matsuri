async function searchFestival(e) {
  e.preventDefault();
  const city = document.getElementById("cityInput").value;
  const loading = document.getElementById("loading");
  const resultsDiv = document.getElementById("results");
  const calendar = document.getElementById("calendar");
  loading.style.display = "block";
  resultsDiv.innerHTML = "";
  calendar.innerHTML = "";

  const formData = new FormData();
  formData.append("city", city);

  const res = await fetch("/search", {
    method: "POST",
    body: formData
  });
  const data = await res.json();
  loading.style.display = "none";

  if (data.length === 0) {
    resultsDiv.innerHTML = "<p>該当する祭りは見つかりませんでした。</p>";
    return;
  }

  resultsDiv.innerHTML = "<h2>検索結果</h2><ul>" + data.map(f =>
    `<li><a href="${f.link}" target="_blank">${f.title}</a> (${f.date})</li>`
  ).join("") + "</ul>";

  const eventsByDate = {};
  data.forEach(f => {
    const match = f.date.match(/\d{4}年?\d{1,2}月?\d{1,2}日?/);
    if (match) {
      const dateStr = match[0].replace(/[年月]/g, "-").replace("日", "");
      eventsByDate[dateStr] = eventsByDate[dateStr] || [];
      eventsByDate[dateStr].push(f.title);
    }
  });

  const today = dayjs();
  let html = "<tr><th>日付</th><th>イベント</th></tr>";
  for (let i = 0; i < 30; i++) {
    const d = today.add(i, "day").format("YYYY-MM-DD");
    const events = eventsByDate[d] || [];
    html += `<tr${events.length ? ' class="highlight"' : ''}><td>${d}</td><td>${events.join("<br>")}</td></tr>`;
  }
  calendar.innerHTML = html;
}
