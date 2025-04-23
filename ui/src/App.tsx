import { SWRConfig } from "swr";
import Router from "./router";
import { get } from "./api";
import { Toaster } from "sonner";

function App() {
  return (
    <SWRConfig
      value={{
        fetcher: get,
        errorRetryCount: 1,
      }}
    >
      <Router />

      <Toaster />
    </SWRConfig>
  );
}

export default App;
