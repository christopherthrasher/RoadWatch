"use client";

import { Disclosure, DisclosurePanel, DisclosureButton } from "@headlessui/react";
import Link from "next/link";
import Image from "next/image";

interface LinkProps {
  text: string;
  href: string;
  external: boolean;
}

interface DisclosureClientProps {
  topnav: {
    logoLink: {
      text: string;
      href: string;
      image: {
        url: string;
        alternativeText: string | null;
        name: string;
      };
    };
    link: LinkProps[];
  };
}

export function DisclosureClient(props: Readonly<DisclosureClientProps>) {
  const navigation = props.topnav.link;
  const logo = props.topnav.logoLink;

  return (
    <Disclosure>
      {({ open }: {open: Boolean}) => (
        <div className="flex flex-wrap items-center justify-between h-full lg:w-auto">
          {/* LOGO and Website Name, left side */}
          <Link href={logo.href || "/"}>
            <span className="flex items-center space-x-2 text-2xl font-medium text-main-primary">
              <span>
                <Image
                  src={logo.image.url}
                  alt={logo.image.alternativeText || logo.image.name}
                  width={32}
                  height={32}
                  className="w-8"
                  loading="eager"
                  priority={true}
                />
              </span>
              <span>{logo.text}</span>
            </span>
          </Link>
          {/* Pancake stack for navigation when they are on smaller devices */}
          <DisclosureButton
            aria-label="Toggle Menu"
            className="px-2 py-1 ml-auto text-main-text rounded-md lg:hidden hover:text-main-secondary focus:text-main-primary focus:bg-main-bg-secondary focus:outline-none"
          >
            <svg
              className="w-6 h-6 fill-current"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
            >
              {open && (
                <path
                  fillRule="evenodd"
                  clipRule="evenodd"
                  d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"
                />
              )}
              {!open && (
                <path
                  fillRule="evenodd"
                  d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"
                />
              )}
            </svg>
          </DisclosureButton>
          {/* Content inside that is shown when pancake is open */}
          <DisclosurePanel className="flex flex-wrap w-full my-5 lg:hidden">
            <>
              {navigation.map((item, index) => (
                <Link
                  key={index}
                  href={item.href}
                  className="w-full px-4 py-2 -ml-4 text-main-text rounded-md hover:text-main-secondary focus:text-main-primary focus:bg-main-bg-secondary focus:outline-none"
                >
                  {item.text}
                </Link>
              ))}
            </>
          </DisclosurePanel>
        </div>
      )}
    </Disclosure>
  );
}