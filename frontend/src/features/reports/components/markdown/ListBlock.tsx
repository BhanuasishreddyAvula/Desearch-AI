import React from 'react';
import type { ListNode } from '../../utils/markdownParser';
import { InlineRenderer } from './InlineRenderer';

interface ListBlockProps {
  node: ListNode;
}

export const ListBlock: React.FC<ListBlockProps> = ({ node }) => {
  const { ordered, items } = node;

  const ListTag = ordered ? 'ol' : 'ul';
  const listClasses = ordered
    ? 'list-decimal pl-5 space-y-2 mb-5 font-sans-ui text-sm md:text-base leading-relaxed text-foreground/90 select-text'
    : 'list-disc marker:text-accent pl-5 space-y-2 mb-5 font-sans-ui text-sm md:text-base leading-relaxed text-foreground/90 select-text';

  return (
    <ListTag className={listClasses}>
      {items.map((itemText, idx) => (
        <li key={idx} className="animate-in fade-in duration-100 pl-1">
          <InlineRenderer text={itemText} />
        </li>
      ))}
    </ListTag>
  );
};
