import keysFixture from "@/mocks/fixtures/keys-list.json";
import teamsFixture from "@/mocks/fixtures/teams-list.json";
import usersFixture from "@/mocks/fixtures/users-list.json";
import orgsFixture from "@/mocks/fixtures/organizations-list.json";

type KeysResponse = typeof keysFixture;
type TeamsResponse = typeof teamsFixture;
type UsersResponse = typeof usersFixture;

let keysState: KeysResponse = structuredClone(keysFixture);
let teamsState: TeamsResponse = structuredClone(teamsFixture);
let usersState: UsersResponse = structuredClone(usersFixture);
let orgsState = structuredClone(orgsFixture);

export function resetMockStore(): void {
  keysState = structuredClone(keysFixture);
  teamsState = structuredClone(teamsFixture);
  usersState = structuredClone(usersFixture);
  orgsState = structuredClone(orgsFixture);
}

export function getKeysList(): KeysResponse {
  return keysState;
}

export function deleteKey(tokenId: string): void {
  keysState = {
    ...keysState,
    keys: keysState.keys.filter((k) => k.token_id !== tokenId),
    total_count: Math.max(0, keysState.total_count - 1),
  };
}

export function addKey(key: KeysResponse["keys"][0]): void {
  keysState = {
    ...keysState,
    keys: [key, ...keysState.keys],
    total_count: keysState.total_count + 1,
  };
}

export function getTeamsList(): TeamsResponse {
  return teamsState;
}

export function getUsersList(): UsersResponse {
  return usersState;
}

export function getOrganizationsList(): typeof orgsState {
  return orgsState;
}
