import Link from "next/link";
import { DisclosureClient } from "@/components/DisclosureClient";

async function loader() {

  const data = {
    id: 1,
    topnav: {
      id: 1,
      logoLink: {
        id: 1,
        text: 'RoadWatch',
        href: '/',
        image: {
          id: 1,
          url: '/img/logo.svg',
          alternativeText: null,
          name: 'logo.svg'
        }
      },
      link: [
        { id: 1, href: '/', text: 'Map', external: false },
        { id: 3, href: '/upload', text: 'Upload', external: false },
        { id: 4, href: '/review', text: 'Review', external: false },
        { id: 4, href: '/maintenance', text: 'Maintenance', external: false }
      ]
    }
  }
  
  
  return data;
}

interface NavbarData {
  id: number;
  topnav: {
    id: number;
    logoLink: {
      id: number;
      text: string;
      href: string;
      image: {
        id: number;
        url: string;
        alternativeText: string | null;
        name: string;
      };
    };
    link: {
      id: number;
      href: string;
      text: string;
      external: boolean;
    }[];
  };
}

export async function Navbar() {
  const data = await loader() as NavbarData;
  if (!data) return null;
  const navigation = data.topnav.link;

  return (
    <div className="lg:min-h-screen lg:w-auto w-full bg-main-bg-secondary p-4">
      <nav className="container relative flex-col items-center justify-between p-8 lg:justify-between xl:px-0">
        {/* Logo  */}

        <DisclosureClient topnav={data.topnav} />

        {/* Nav links  */}
        <div className="hidden text-center lg:flex lg:items-center">
          <ul className="items-center justify-end pt-6 list-none lg:pt-0 lg:flex-col">
            {navigation.map((menu, index) => (
              <li className="mr-3" key={index}>
                <Link
                  href={menu.href}
                  className="inline-block px-4 py-2 text-lg font-normal text-main-text no-underline rounded-md hover:text-main-secondary focus:text-main-primary focus:bg-main-bg-secondary focus:outline-none"
                >
                  {menu.text}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </nav>
    </div>
  );
}







/* 
export async function Navbar() {
  const data = await loader() as NavbarData;
  if (!data) return null;
  const navigation = data.topnav.link;

  return (
    <>
      <aside className="hidden flex-col border-r border-main-bg-secondary bg-main-surface px-5 py-6 lg:flex min-h-screen w-auto">
        <DisclosureClient topnav={data.topnav} />
        <nav aria-label="Main navigation" className="mt-8">
          <ul className="flex flex-col gap-2">
            {navigation.map((menu) => (
              <li key={menu.href}>
                <Link
                  href={menu.href}
                  className="block rounded-md px-4 py-3 text-main-text hover:bg-main-bg-secondary hover:text-main-primary focus:bg-main-bg-secondary focus:text-main-primary focus:outline-none"
                >
                  {menu.text}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
      <header className="sticky top-0 z-40 border-b border-main-bg-secondary bg-main-surface px-4 py-3 lg:hidden">
        <DisclosureClient topnav={data.topnav} />
      </header>
    </>
  );
}



*/