interface HeritageLogoProps {
  size?: number;
}

export function HeritageLogo({ size = 64 }: HeritageLogoProps) {
  const height = Math.round((size * 46) / 64);
  return (
    <svg
      width={size}
      height={height}
      viewBox="0 0 212.121 151.515"
      style={{ shapeRendering: "crispEdges" }}
      aria-hidden="true"
    >
      <rect x="30" y="0" width="30" height="30" fill="#FFAF01" />
      <rect x="152" y="0" width="30" height="30" fill="#FFAF01" />
      <rect x="30" y="30" width="60" height="30" fill="#FF8204" />
      <rect x="121" y="30" width="60" height="30" fill="#FF8204" />
      <rect x="30" y="61" width="152" height="30" fill="#FA500F" />
      <rect x="30" y="91" width="30" height="30" fill="#E51300" />
      <rect x="91" y="91" width="30" height="30" fill="#E51300" />
      <rect x="152" y="91" width="30" height="30" fill="#E51300" />
      <rect x="0" y="121" width="91" height="30" fill="#C4001D" />
      <rect x="121" y="121" width="91" height="30" fill="#C4001D" />
    </svg>
  );
}