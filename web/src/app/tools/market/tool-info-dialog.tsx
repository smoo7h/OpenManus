import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { forwardRef, useImperativeHandle, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';
import { ToolConfigDialog, ToolConfigDialogRef } from './tool-config-dialog';
import { Tools } from '@prisma/client';

export interface ToolInfoDialogRef {
  showInfo: (tool: Tools) => void;
}

interface ToolInfoDialogProps {
  onConfigSuccess: () => void;
}

export const ToolInfoDialog = forwardRef<ToolInfoDialogRef, ToolInfoDialogProps>((props, ref) => {
  const [open, setOpen] = useState(false);
  const [tool, setTool] = useState<Tools>();
  const toolConfigDialogRef = useRef<ToolConfigDialogRef>(null);
  useImperativeHandle(ref, () => ({
    showInfo: (tool: Tools) => {
      setTool(tool);
      setOpen(true);
    },
  }));

  if (!tool) {
    return null;
  }

  return (
    <>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent style={{ height: '800px', width: '1200px', maxWidth: 1200, overflowY: 'hidden', display: 'flex', flexDirection: 'column' }}>
          <DialogHeader>
            <DialogTitle className="text-2xl font-bold">{tool.name}</DialogTitle>
            <div className="mt-2">
              <Button variant="default" size="sm" className="w-full sm:w-auto" onClick={() => toolConfigDialogRef.current?.showConfig(tool!)}>
                Install Tool
              </Button>
            </div>
          </DialogHeader>
          <div className="markdown-body text-wrap">
            <Markdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
              components={{
                a: ({ href, children }) => {
                  return (
                    <a href={href} target="_blank" rel="noopener noreferrer">
                      {children}
                    </a>
                  );
                },
              }}
            >
              {tool.description}
            </Markdown>
          </div>
        </DialogContent>
      </Dialog>
      <ToolConfigDialog ref={toolConfigDialogRef} onSuccess={props.onConfigSuccess} />
    </>
  );
});
