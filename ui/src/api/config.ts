import Axios from "axios";
import { getToken, removeToken } from "./token";

export const BaseUrl = import.meta.env.VITE_API_BASE_URL;
export const apiAgent = Axios.create({ baseURL: BaseUrl });

apiAgent.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token && config.headers && !config.headers?.Authorization) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiAgent.interceptors.response.use(
  (config) => config,
  (error) => {
    if (error.response?.status === 401) {
      removeToken();
    }

    return Promise.reject(error);
  }
);
