import type { Metadata } from "next";
import { Instrument_Serif, IBM_Plex_Sans, IBM_Plex_Mono } from "next/font/google";
import { PLUGIN_VERSION, BRAND_COLOR } from "@/lib/plugin-version";
import "./globals.css";

const instrumentSerif = Instrument_Serif({
  variable: "--font-instrument-serif",
  subsets: ["latin"],
  weight: "400",
});

const ibmPlexSans = IBM_Plex_Sans({
  variable: "--font-ibm-plex-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

const ibmPlexMono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-mono",
  subsets: ["latin"],
  weight: ["400", "500"],
});

const SITE_URL = "https://frontend-taste-engineer.vercel.app";

export const metadata: Metadata = {
  title: "Frontend Taste Engineer — Give it one sentence. Get a frontend with taste.",
  description:
    "An installable Codex plugin that turns minimal frontend requests into complete, context-aware, responsive, accessible, screenshot-refined, deployment-ready implementations.",
  metadataBase: new URL(SITE_URL),
  openGraph: {
    title: "Frontend Taste Engineer",
    description:
      "Turn minimal frontend prompts into complete, context-aware web experiences with taste.",
    url: SITE_URL,
    siteName: "Frontend Taste Engineer",
    type: "website",
    images: [
      {
        url: "/assets/logo.svg",
        width: 560,
        height: 144,
        alt: "Frontend Taste Engineer",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Frontend Taste Engineer",
    description:
      "Turn minimal frontend prompts into complete, context-aware web experiences with taste.",
    images: ["/assets/logo.svg"],
  },
  icons: {
    icon: "/assets/icon.svg",
    apple: "/assets/icon.svg",
  },
  other: {
    "theme-color": BRAND_COLOR,
    "plugin-version": PLUGIN_VERSION,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${instrumentSerif.variable} ${ibmPlexSans.variable} ${ibmPlexMono.variable} scroll-smooth`}
    >
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
