import type { Metadata } from "next";
import "./styles.css";
export const metadata: Metadata = { title: "Employee Portal | Day 7", description: "Next.js employee portal training project" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
