import { AxiosResponse } from "axios";

export function onSuccess<T>(response: AxiosResponse<T>) {
  return response.data;
}

export function onError(error: unknown) {
  let errorMessage = "An unknown error occurred";

  if (typeof error === "object" && error !== null) {
    if ("response" in error) {
      errorMessage = (error as { response: string }).response;
    } else if ("message" in error) {
      errorMessage = (error as { message: string }).message;
    }
  }

  const errorObject = new Error(errorMessage);
  console.error("Request Failed:", errorObject);

  return Promise.reject(errorObject);
}
