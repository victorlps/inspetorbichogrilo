import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const BenchScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const cardIn = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 130, mass: 0.8 },
  });

  const step2In = spring({
    frame: Math.max(0, frame - 24),
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  const step3In = spring({
    frame: Math.max(0, frame - 52),
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  const barFresh = interpolate(frame, [10, 45], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const barFreeze = interpolate(frame, [28, 65], [0, 12], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const visemas = ["X", "A", "OU", "EI", "BMP", "FV", "SORRISO"];
  const activeVisema = visemas[Math.floor(frame / 4) % visemas.length];
  const breatheY = Math.sin(t * 2.6) * 4;
  const lupaRot = -8 + Math.sin(t * 2.1) * 6;

  const captionGroups = [
    { start: 0, end: 29, words: ["Por", "que", "levar"], active: 1 },
    { start: 30, end: 59, words: ["90%", "menos", "peso"], active: 0 },
    { start: 60, end: 89, words: ["na", "sua", "mochila?"], active: 2 },
    { start: 90, end: 120, words: ["Sublimação", "a", "vácuo!"], active: 0 },
  ];
  const currentCap =
    captionGroups.find((c) => frame >= c.start && frame <= c.end) ||
    captionGroups[0];

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 50% 28%, #1e3a2f 0%, #0f1f1c 52%, #080d0e 100%)",
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif',
        color: "#f8fafc",
      }}
    >
      {/* Subtle animated mountain ridge SVG background */}
      <svg
        width="1080"
        height="1920"
        viewBox="0 0 1080 1920"
        style={{ position: "absolute", inset: 0, opacity: 0.26 }}
      >
        <defs>
          <linearGradient id="mtGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#34d399" stopOpacity="0.35" />
            <stop offset="100%" stopColor="#080d0e" stopOpacity="0.0" />
          </linearGradient>
        </defs>
        <path
          d={`M0,980 L220,${780 + Math.sin(t) * 8} L460,910 L740,${710 + Math.cos(t) * 8} L1080,890 L1080,1500 L0,1500 Z`}
          fill="url(#mtGrad)"
        />
      </svg>

      {/* Safe Zone Container: X=65..887, Y=288..1247 */}
      <div
        style={{
          position: "absolute",
          left: 65,
          top: 296,
          width: 822,
          height: 945,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        {/* Top Benefit Pill */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 14,
            alignSelf: "flex-start",
            background: "rgba(15, 23, 42, 0.86)",
            border: "2px solid rgba(52, 211, 153, 0.55)",
            borderRadius: 999,
            padding: "12px 26px",
            transform: `translateY(${(1 - cardIn) * -28}px) scale(${0.92 + 0.08 * cardIn})`,
            opacity: cardIn,
            boxShadow: "0 14px 34px rgba(0,0,0,0.42)",
          }}
        >
          <div
            style={{
              width: 14,
              height: 14,
              borderRadius: 99,
              background: "#34d399",
              boxShadow: "0 0 14px #34d399",
            }}
          />
          <span
            style={{
              fontSize: 27,
              fontWeight: 800,
              letterSpacing: 0.4,
              color: "#ecfdf5",
            }}
          >
            TRILHA LEVE: 90% MENOS PESO NA MOCHILA
          </span>
        </div>

        {/* Main Process + Weight Card */}
        <div
          style={{
            marginTop: 22,
            background: "rgba(15, 23, 42, 0.82)",
            border: "1.5px solid rgba(255,255,255,0.14)",
            borderRadius: 32,
            padding: "32px 34px",
            transform: `scale(${0.94 + 0.06 * cardIn})`,
            opacity: cardIn,
            boxShadow: "0 28px 60px rgba(0,0,0,0.5)",
          }}
        >
          <div
            style={{
              fontSize: 24,
              fontWeight: 700,
              color: "#fbbf24",
              textTransform: "uppercase",
              letterSpacing: 1.2,
              marginBottom: 20,
            }}
          >
            Como a Liofilização Funciona
          </div>

          {/* 3 Animated Process Nodes */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 14,
              marginBottom: 32,
            }}
          >
            {[
              {
                label: "1. Gelo Rápido",
                sub: "-40 °C preserva células",
                prog: cardIn,
                accent: "#38bdf8",
              },
              {
                label: "2. Alto Vácuo",
                sub: "Gelo vira vapor direto",
                prog: step2In,
                accent: "#a78bfa",
              },
              {
                label: "3. Crocante",
                sub: "100% fruta · 0 água",
                prog: step3In,
                accent: "#34d399",
              },
            ].map((item, idx) => (
              <div
                key={idx}
                style={{
                  flex: 1,
                  background: "rgba(30, 41, 59, 0.88)",
                  border: `2px solid ${item.accent}`,
                  borderRadius: 22,
                  padding: "18px 16px",
                  transform: `translateY(${(1 - item.prog) * 20}px)`,
                  opacity: item.prog,
                }}
              >
                <div
                  style={{ fontSize: 25, fontWeight: 800, color: item.accent }}
                >
                  {item.label}
                </div>
                <div
                  style={{
                    fontSize: 20,
                    color: "#cbd5e1",
                    marginTop: 6,
                    fontWeight: 600,
                  }}
                >
                  {item.sub}
                </div>
              </div>
            ))}
          </div>

          {/* Weight Comparison Bars */}
          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            <div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  fontSize: 23,
                  fontWeight: 700,
                  marginBottom: 6,
                }}
              >
                <span>Fruta In Natura (água pura)</span>
                <span style={{ color: "#f87171" }}>500 g</span>
              </div>
              <div
                style={{
                  height: 22,
                  background: "rgba(255,255,255,0.09)",
                  borderRadius: 99,
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    width: `${barFresh}%`,
                    height: "100%",
                    background: "linear-gradient(90deg, #ef4444, #f97316)",
                    borderRadius: 99,
                  }}
                />
              </div>
            </div>

            <div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  fontSize: 23,
                  fontWeight: 700,
                  marginBottom: 6,
                }}
              >
                <span>Equivalente Liofilizado</span>
                <span style={{ color: "#34d399" }}>50 g (-90%)</span>
              </div>
              <div
                style={{
                  height: 22,
                  background: "rgba(255,255,255,0.09)",
                  borderRadius: 99,
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    width: `${barFreeze}%`,
                    height: "100%",
                    background: "linear-gradient(90deg, #10b981, #34d399)",
                    borderRadius: 99,
                  }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Bottom area: Inspector Rig PiP + Dynamic Captions (Y=1040..1220) */}
        <div
          style={{
            position: "relative",
            height: 280,
            display: "flex",
            alignItems: "flex-end",
          }}
        >
          {/* Inspector 2.5D Rig PiP on left */}
          <div
            style={{
              position: "relative",
              width: 230,
              height: 308,
              transform: `translateY(${breatheY}px)`,
              flexShrink: 0,
            }}
          >
            <Img
              src={staticFile("rig/torso_apontar.png")}
              style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
            />
            <Img
              src={staticFile("rig/cabeca_base.png")}
              style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
            />
            <Img
              src={staticFile("rig/antena_esq.png")}
              style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
            />
            <Img
              src={staticFile("rig/antena_dir.png")}
              style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
            />
            <Img
              src={staticFile("rig/haste_lupa.png")}
              style={{
                position: "absolute",
                inset: 0,
                width: "100%",
                height: "100%",
                transformOrigin: "63.8% 15%",
                transform: `rotate(${lupaRot}deg)`,
              }}
            />
            <Img
              src={staticFile("rig/sobrancelha_esq.png")}
              style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
            />
            <Img
              src={staticFile("rig/sobrancelha_dir.png")}
              style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
            />
            <Img
              src={staticFile(`rig/visemas/visema_${activeVisema}.png`)}
              style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
            />
          </div>

          {/* Dynamic 1-3 word caption box inside Y=1040..1220 */}
          <div
            style={{
              flex: 1,
              marginLeft: 12,
              marginBottom: 34,
              background: "rgba(9, 13, 22, 0.90)",
              border: "2px solid rgba(250, 204, 21, 0.45)",
              borderRadius: 24,
              padding: "20px 24px",
              display: "flex",
              flexWrap: "wrap",
              justifyContent: "center",
              gap: 14,
              boxShadow: "0 16px 36px rgba(0,0,0,0.55)",
            }}
          >
            {currentCap.words.map((w, i) => {
              const isAct = i === currentCap.active;
              return (
                <span
                  key={i}
                  style={{
                    fontSize: 44,
                    fontWeight: 900,
                    color: isAct ? "#facc15" : "#ffffff",
                    textDecoration: isAct ? "underline" : "none",
                    textUnderlineOffset: 8,
                    transform: isAct ? "scale(1.07)" : "scale(1.0)",
                    display: "inline-block",
                  }}
                >
                  {w}
                </span>
              );
            })}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
