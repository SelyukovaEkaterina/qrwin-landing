/// <reference path="../.astro/types.d.ts" />

interface Window {
  ymGoal?: (goal: string, params?: Record<string, string | number | boolean>) => void;
}
