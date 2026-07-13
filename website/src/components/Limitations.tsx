import { SectionHeading } from "@/components/ui/SectionHeading";

const LIMITATIONS = [
  "Static checks cannot prove full screen-reader or real-device behavior",
  "Pixel accuracy requires same-viewport visual comparison",
  "Framework and browser guidance must be rechecked as versions change",
  "Some visual or social sources may be inaccessible or license-ambiguous",
  "Most catalog sources remain unresolved until item-level review",
  "The private-term scanner cannot inspect text rendered inside raster screenshots",
  "The Apps SDK registration step remains manual",
];

export function Limitations() {
  return (
    <section className="section-padding bg-paper-elevated border-y border-line">
      <div className="container-main">
        <SectionHeading title="Verified where possible. Honest where it is not." />

        <ul className="space-y-4 max-w-3xl">
          {LIMITATIONS.map((limitation) => (
            <li
              key={limitation}
              className="flex gap-4 text-sm text-gray-600 leading-relaxed border-l-2 border-gold/60 pl-4"
            >
              {limitation}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
