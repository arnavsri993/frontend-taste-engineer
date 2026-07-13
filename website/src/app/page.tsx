import { Navigation } from "@/components/Navigation";
import { Hero } from "@/components/Hero";
import { TasteLabDemo } from "@/components/TasteLabDemo";
import { ProblemStatement } from "@/components/ProblemStatement";
import { CapabilitySystem } from "@/components/CapabilitySystem";
import { Workflow } from "@/components/Workflow";
import { ContextAdaptiveTaste } from "@/components/ContextAdaptiveTaste";
import { Architecture } from "@/components/Architecture";
import { SafeSourceUse } from "@/components/SafeSourceUse";
import { SupportedWork } from "@/components/SupportedWork";
import { StarterPrompts } from "@/components/StarterPrompts";
import { Installation } from "@/components/Installation";
import { Limitations } from "@/components/Limitations";
import { FAQ } from "@/components/FAQ";
import { FinalCTA } from "@/components/FinalCTA";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Navigation />
      <main>
        <Hero />
        <TasteLabDemo />
        <ProblemStatement />
        <CapabilitySystem />
        <Workflow />
        <ContextAdaptiveTaste />
        <Architecture />
        <SafeSourceUse />
        <SupportedWork />
        <StarterPrompts />
        <Installation />
        <Limitations />
        <FAQ />
        <FinalCTA />
      </main>
      <Footer />
    </>
  );
}
