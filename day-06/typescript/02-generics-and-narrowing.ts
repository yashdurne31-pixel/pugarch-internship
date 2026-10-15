function firstItem<T>(items: T[]): T | undefined {
  return items[0];
}

type ApiResult<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function printResult<T>(result: ApiResult<T>): void {
  if (result.success) {
    console.log("Result:", result.data);
  } else {
    console.error("Request failed:", result.error);
  }
}

console.log(firstItem<number>([10, 20, 30]));
printResult<string>({ success: true, data: "Type narrowing works" });
printResult<number>({ success: false, error: "Example error" });
