import { get, post } from ".";

export type UserType = {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: number;
};

export const login = (data: { username: string; password: string }) => {
  const formData = new FormData();

  formData.append("username", data.username);
  formData.append("password", data.password);

  return post<{
    access_token: string;
    token_type: string;
  }>("/auth/access-token", formData);
};

export const getMe = () => {
  return get<UserType>("/users/me");
};
