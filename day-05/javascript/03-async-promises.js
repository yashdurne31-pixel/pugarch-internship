const wait = milliseconds =>
  new Promise(resolve => setTimeout(resolve, milliseconds));

async function runExample() {
  try {
    console.log("Starting asynchronous task...");
    await wait(500);
    console.log("Task completed.");
  } catch (error) {
    console.error("Task failed:", error.message);
  }
}

runExample();
