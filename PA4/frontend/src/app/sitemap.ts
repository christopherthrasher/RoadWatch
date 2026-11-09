import { MetadataRoute } from "next";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
    return [
        {
            url: "/", //this would be domain
            lastModified: new Date(),
            priority: 1
        }
    ]
}