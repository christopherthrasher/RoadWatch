This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

RoadWatch frontend source and frontend tests.

**First, run the development server without docker**:

```bash
# Run this to install all required packages using npm
npm ci
# run this to run dev version
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

**Run production version with docker**:

From the PA4 directory, create the shared network and start the backend:

```bash
docker network create proxy-net
docker compose up -d --build
```

If Docker reports that `proxy-net` already exists, continue with the Compose command.

if running from frontend directory run:

```bash
docker compose -f docker-compose.yaml up -d --build
```

Open [http://localhost:3000](http://localhost:3000) to use the website.

## Installing required packages

When running the project locally and not inside of docker container
The packages must be locally installed
ensure your terminal is located inside the frontend folder
then run the following commands
Note: this requires node to be installed on your computer

```bash
npm ci
```

installing the packages allows for running the dev version on your computer with
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

## Running Tests

vitest has been implemented into the project.
Running the following command will run all current tests that have been made with .test.tsx

```bash
npm run test
```

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.