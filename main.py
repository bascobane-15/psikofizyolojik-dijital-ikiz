import { useState } from "react";

export default function App() {
  const [task, setTask] = useState(5);
  const [sleep, setSleep] = useState(7);
  const [social, setSocial] = useState(5);
  const [light, setLight] = useState(12);

  // --- BASİT AMA BİLİMSEL MANTIK ---
  const PSI = Math.round(
    task * 6 +
    (10 - sleep) * 4 +
    (10 - social) * 3 +
    Math.abs(light - 12) * 2
  );

  const FYI = Math.round(
    task * 5 +
    (10 - sleep) * 5 +
    Math.abs(light - 12) * 3
  );

  const BPRS = Math.round((PSI + FYI) / 2);

  const riskColor =
    BPRS < 34 ? "#22c55e" : BPRS < 67 ? "#eab308" : "#ef4444";

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(180deg, #020617, #020024)",
      color: "white",
      padding: "30px",
      fontFamily: "Arial"
    }}>
      <h1>❄️ PolarTwin</h1>
      <p>Dijital İkiz Psikofizyolojik Risk Simülasyonu</p>

      {/* KONTROLLER */}
      <div style={{ maxWidth: 500 }}>
        <label>Görev Yoğunluğu: {task}</label>
        <input type="range" min="0" max="10" value={task}
          onChange={e => setTask(+e.target.value)} />

        <label>Uyku Süresi (saat): {sleep}</label>
        <input type="range" min="4" max="9" value={sleep}
          onChange={e => setSleep(+e.target.value)} />

        <label>Sosyal Etkileşim: {social}</label>
        <input type="range" min="0" max="10" value={social}
          onChange={e => setSocial(+e.target.value)} />

        <label>Işık / Fotoperiyod (saat): {light}</label>
        <input type="range" min="0" max="24" value={light}
          onChange={e => setLight(+e.target.value)} />
      </div>

      {/* SONUÇLAR */}
      <div style={{
        marginTop: 30,
        padding: 20,
        borderRadius: 12,
        background: "rgba(255,255,255,0.08)"
      }}>
        <h3>Psikolojik Stres İndeksi (PSI): {PSI}</h3>
        <h3>Fizyolojik Yüklenme İndeksi (FYI): {FYI}</h3>

        <h2 style={{ color: riskColor }}>
          BPRS: {BPRS}
        </h2>
        <strong style={{ color: riskColor }}>
          {BPRS < 34 ? "DÜŞÜK RİSK" : BPRS < 67 ? "ORTA RİSK" : "YÜKSEK RİSK"}
        </strong>
      </div>
    </div>
  );
}
