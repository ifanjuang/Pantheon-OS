import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ARCEUS Control",
  description: "Control plane — visibilité système en temps réel",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="min-h-screen bg-surface text-zinc-200">{children}</body>
    </html>
  );
}
