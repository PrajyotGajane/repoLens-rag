import type { Components } from "react-markdown";

/** Explicit styles so markdown renders correctly without relying only on `prose`. */
export const assistantMarkdownComponents: Components = {
  p: ({ children }) => (
    <p className="mb-3 text-[0.9375rem] leading-relaxed last:mb-0">{children}</p>
  ),
  strong: ({ children }) => (
    <strong className="font-semibold text-zinc-50">{children}</strong>
  ),
  em: ({ children }) => <em className="italic">{children}</em>,
  h1: ({ children }) => (
    <h1 className="mt-4 mb-2 text-xl font-semibold text-zinc-50 first:mt-0">
      {children}
    </h1>
  ),
  h2: ({ children }) => (
    <h2 className="mt-3 mb-2 text-lg font-semibold text-zinc-50 first:mt-0">
      {children}
    </h2>
  ),
  h3: ({ children }) => (
    <h3 className="mt-2 mb-1 text-base font-semibold text-zinc-100 first:mt-0">
      {children}
    </h3>
  ),
  ul: ({ children }) => (
    <ul className="my-2 list-disc space-y-1 pl-5 text-[0.9375rem] leading-relaxed">
      {children}
    </ul>
  ),
  ol: ({ children }) => (
    <ol className="my-2 list-decimal space-y-1 pl-5 text-[0.9375rem] leading-relaxed">
      {children}
    </ol>
  ),
  li: ({ children }) => <li className="leading-relaxed">{children}</li>,
  blockquote: ({ children }) => (
    <blockquote className="my-2 border-l-2 border-white/25 pl-3 text-zinc-300">
      {children}
    </blockquote>
  ),
  a: ({ href, children }) => (
    <a
      href={href}
      className="text-emerald-400 underline decoration-emerald-400/40 underline-offset-2 hover:text-emerald-300"
      target="_blank"
      rel="noopener noreferrer"
    >
      {children}
    </a>
  ),
  hr: () => <hr className="my-4 border-white/15" />,
  pre: ({ children }) => (
    <pre className="my-3 overflow-x-auto rounded-lg border border-white/10 bg-black/45 p-3 text-xs leading-relaxed">
      {children}
    </pre>
  ),
  code: ({ className, children, ...props }) => {
    const isBlock =
      typeof className === "string" && /\blanguage-/.test(className);
    if (isBlock) {
      return (
        <code className={className} {...props}>
          {children}
        </code>
      );
    }
    return (
      <code
        className="rounded bg-white/10 px-1.5 py-0.5 font-mono text-[0.85em] text-zinc-100"
        {...props}
      >
        {children}
      </code>
    );
  },
  table: ({ children }) => (
    <div className="my-3 overflow-x-auto rounded-lg border border-white/10">
      <table className="min-w-full border-collapse text-left text-[0.875rem]">
        {children}
      </table>
    </div>
  ),
  thead: ({ children }) => (
    <thead className="border-b border-white/10 bg-white/5">{children}</thead>
  ),
  tbody: ({ children }) => <tbody>{children}</tbody>,
  tr: ({ children }) => <tr className="border-b border-white/10 last:border-0">{children}</tr>,
  th: ({ children }) => (
    <th className="border border-white/10 px-3 py-2 font-medium text-zinc-100">
      {children}
    </th>
  ),
  td: ({ children }) => (
    <td className="border border-white/10 px-3 py-2 text-zinc-200">{children}</td>
  ),
};
