import type { Status } from "../types";

export default function StatusBar({ status }: { status: Status }) {
  return (
    <div className="p-2 text-sm text-gray-400">
      Status: {status}
    </div>
  );
}