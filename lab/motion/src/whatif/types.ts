// One "What if" POV film: chained AI clips under a readout, a title and short captions.
export type Caption = {
  readonly from: number; // seconds
  readonly to: number;
  readonly text: string;
};

export type Readout = {
  readonly label: string;
  readonly value: string;
  readonly sub: string;
  readonly opacity: number; // 0..1
};

export type WhatIfFilm = {
  readonly title: string;
  readonly clips: readonly string[]; // paths in public/, played back to back
  readonly clipSeconds: number;
  readonly sound: string; // path in public/
  readonly captions: readonly Caption[];
  readonly readout: (t: number) => Readout; // t in seconds
};
