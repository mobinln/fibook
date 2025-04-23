import { post } from ".";
import { AssetTypeType } from "./asset_type";
import { CurrencyType } from "./currency";

export type AssetType = {
  name: string;
  symbol: string;
  description: string;
  is_active: boolean;
  asset_type_id: number;
  currency_id: number;
  asset_type: AssetTypeType;
  currency: CurrencyType;
  id: number;
  created_at: string;
  updated_at: null | string;
};

export const createAsset = (data: {
  symbol?: string;
  name?: string;
  description?: string;
  is_active?: boolean;
  currency_id?: number;
  asset_type_id?: number;
}) => {
  return post<AssetType>("/assets", data);
};
