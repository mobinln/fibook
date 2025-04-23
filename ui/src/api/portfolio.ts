import { post } from ".";
import { AssetType } from "./assets";

export type PortfolioType = {
  name: string;
  description: string;
  is_active: boolean;
  base_currency_id: number;
  id: number;
  user_id: number;
  created_at: string;
  updated_at: null | string;
};

export type PortfolioHoldingType = {
  quantity: number;
  asset_id: number;
  id: number;
  asset: AssetType;
  avg_purchase_price: number;
};

export const createPortfolio = (data: {
  name: string;
  description: string;
  is_active?: boolean;
  base_currency_id: number;
}) => {
  return post<PortfolioType>("/portfolios", data);
};

export const createHolding = (portfolioId: number | string, data: { asset_id: number; quantity: number }) => {
  return post(`/portfolios/${portfolioId}/holdings`, data);
};
