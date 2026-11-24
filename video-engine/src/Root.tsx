import React from "react";
import { Composition } from "remotion";
import { BenchScene } from "./BenchScene";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="BenchScene"
        component={BenchScene}
        durationInFrames={120}
        fps={24}
        width={1080}
        height={1920}
      />
    </>
  );
};
